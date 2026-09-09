program palindrome_change
  implicit none
  integer :: arr_len, i, result
  integer, allocatable :: arr(:)

  ! Read input
  read(*,*) arr_len
  allocate(arr(arr_len))
  do i = 1, arr_len
    read(*,*) arr(i)
  end do

  ! Calculate minimum changes needed to make array palindromic
  result = 0
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      result = result + 1
    end if
  end do

  ! Output result
  print *, result

end program palindrome_change