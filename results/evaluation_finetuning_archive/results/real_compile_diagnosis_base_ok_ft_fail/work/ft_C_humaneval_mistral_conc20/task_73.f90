program palindrome_changes
  implicit none
  integer :: arr_len, i, changes
  integer, allocatable :: arr(:)
  
  ! Read input
  read(*,*) arr_len
  allocate(arr(arr_len))
  read(*,*) arr
  
  ! Calculate minimum changes needed
  changes = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      changes = changes + 1
    end if
  end do
  
  ! Output result
  print*, changes
end program palindrome_changes