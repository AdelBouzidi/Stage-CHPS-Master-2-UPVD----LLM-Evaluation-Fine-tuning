program palindrome_change
  implicit none
  integer, parameter :: max_len = 100
  integer :: arr_len
  integer :: arr(max_len)
  integer :: result
  integer :: i

  ! Read input
  read(*, *) arr_len
  read(*, *) arr

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