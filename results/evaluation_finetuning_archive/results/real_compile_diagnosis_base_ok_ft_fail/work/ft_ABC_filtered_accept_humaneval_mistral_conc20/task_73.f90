program palindrome_change
  implicit none
  integer, parameter :: max_len = 100
  integer :: arr_len
  integer :: arr(max_len)
  integer :: i, changes

  ! Read array length
  read(*,*) arr_len

  ! Read array elements
  do i = 1, arr_len
    read(*,*) arr(i)
  end do

  ! Calculate minimum changes needed
  changes = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      changes = changes + 1
    end if
  end do

  ! Output result
  print *, changes

end program palindrome_change