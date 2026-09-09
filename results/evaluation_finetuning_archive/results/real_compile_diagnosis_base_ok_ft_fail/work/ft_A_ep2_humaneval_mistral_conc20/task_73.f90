program palindrome_change
  implicit none
  integer, parameter :: dp = selected_int_kind(9)
  integer :: arr_len
  integer, allocatable :: arr(:)
  integer :: result

  ! Read input
  read(*,*) arr_len
  allocate(arr(arr_len))
  read(*,*) arr

  ! Calculate minimum changes to make palindrome
  result = 0
  integer :: i
  do i = 1, arr_len/2
    if (arr(i) /= arr(arr_len - i + 1)) then
      result = result + 1
    end if
  end do

  ! Output result
  print *, result

end program palindrome_change